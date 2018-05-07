from __future__ import print_function

import argparse
import os
import random
import sys

import boto3

__version__ = '1.9.0'

parser = argparse.ArgumentParser(
    description="""
    SSH into an ec2 host where a tag matches the given value. In the case there
    is more than one such instance, one will be chosen at random. Any extra
    arguments are passed to ssh directly.
    """
)
parser.add_argument('-t', '--tag', type=str,
                    default=os.getenv('EC2_HOST_TAG', 'Name'),
                    help="Tag to match, defaults to 'Name'")
parser.add_argument('-u', '--user', type=str,
                    default=os.getenv('EC2_SSH_USER', 'ubuntu'),
                    help="Which user to connect with, defaults to 'ubuntu'")
parser.add_argument('value', help="The value for the tag to match")


def main():
    args, unparsed = parser.parse_known_args()

    if '@' in args.value:
        username, value = args.value.split('@', 1)
    else:
        username = args.user
        value = args.value

    host_name = get_host_name(args.tag, value)

    if not host_name:
        print("ec2-ssh: no hosts matched", file=sys.stderr)
        sys.exit(1)

    command = [
        'ssh',
        '-t', '-t',
        username + '@' + host_name,
    ]
    if unparsed:
        command.extend(unparsed)

    print("ec2-ssh connecting to {}".format(host_name), file=sys.stderr)
    sys.stdout.flush()
    os.execlp(*command)


def get_host_name(tag, value):
    for host in get_dns_names(tag, value):
        return host


def ec2_host_parser():
    parser = argparse.ArgumentParser(
        description="Output ec2 public host names for active hosts in random "
                    "order, optionally match a tag which defaults to 'Name' "
                    "or environment variable EC2_HOST_TAG."
    )
    parser.add_argument('value', type=str, nargs='?',
                        help='the value the tag should equal')
    parser.add_argument('-t', '--tag', type=str,
                        default=os.getenv('EC2_HOST_TAG', 'Name'),
                        help='which tag to search')
    return parser


def host():
    args = ec2_host_parser().parse_args()
    instances = get_dns_names(args.tag, args.value)
    random.shuffle(instances)
    for instance in instances:
        print(instance)


def get_dns_names(tag, value):
    conn = boto3.client('ec2')

    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running'],
        }
    ]
    if value:
        filters.append({
            'Name': 'tag:' + tag,
            'Values': [value]
        })

    data = conn.describe_instances(Filters=filters)

    dns_names = []
    for reservation in data['Reservations']:
        for instance in reservation['Instances']:
            if instance.get('PublicDnsName'):
                dns_names.append(instance['PublicDnsName'])
            elif instance.get('PublicIpAddress'):
                dns_names.append(instance['PublicIpAddress'])
            elif instance['PrivateIpAddress']:
                dns_names.append(instance['PrivateIpAddress'])
    return dns_names


if __name__ == '__main__':
    main()
