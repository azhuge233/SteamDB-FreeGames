import json


def load_json(path, method="r"):
	with open(path, method, encoding='utf-8') as f:
		data = json.load(f)
	return data


def write_json(path, data, method="w"):
	with open(path, method, encoding='utf-8') as f:
		json.dump(data, f, indent=4)