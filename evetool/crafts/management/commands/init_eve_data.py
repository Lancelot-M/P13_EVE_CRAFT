import yaml

def print_file():
    with open(".travis.yml", 'r') as stream:
        try:
            file = yaml.safe_load(stream)
            for el in file["install"]:
                print(el)
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == "__main__":
    print_file()