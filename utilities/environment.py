vars = {}
env = lambda key: vars[key]
path = ".env"

try:
    with open(path, "r") as f:
        for line in f:
            var, value = line.strip().split("=", 1)
            vars[var] = value
except FileNotFoundError:
    print(f"You need to create a {path} file to operate the application! Copy .env.example to {path} and change values if necessary.")

    for line in f:
        line = line.strip()
        if not line or "=" not in line:
            continue
        var, value = line.split("=", 1)