import argparse
from manager import VolumeManager
from volume import Volume, TVolumeCreate, TVolumeMount


parser = argparse.ArgumentParser(description='Secure self-hosted storage service.')


class S4CLI:
    def create_volume(self, *args, **kwrags):
        # config parser for nice help
        create_volume_parser = argparse.ArgumentParser(parents=[parser], conflict_handler='resolve')
        create_volume_parser.add_argument('name', action='store')
        create_volume_parser.add_argument('size', action='store')
        
        # parse cli args
        args = create_volume_parser.parse_args()
        
        v: Volume = VolumeManager.create_volume(TVolumeCreate(args.name, args.size))
        print(v)

    def mount(self, *args, **kwrags):
        # config parser for nice help
        mount_volume_parser = argparse.ArgumentParser(parents=[parser], conflict_handler='resolve')
        mount_volume_parser.add_argument('name', action='store')
        mount_volume_parser.add_argument('mount_point', action='store')

        args = mount_volume_parser.parse_args()
        VolumeManager.mount_volume(TVolumeMount(args.name, args.mount_point))


def main():
    parser.add_argument('command', action='store', choices=[func for func in dir(S4CLI) if callable(getattr(S4CLI, func)) and not func.startswith("__")]
)

    args, command_args = parser.parse_known_args()
    print(args, command_args)

    cli = S4CLI()
    try:
        method = getattr(cli, args.command)
        method(command_args)
    except AttributeError:
        parser.print_help()
if __name__ == '__main__':
    main()