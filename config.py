import os

config_file = os.environ.get("VNNV_CONFIG", "$HOME/.dotfiles/vnnv/config.json")

with open(config_file)
