import subprocess, time
from utilities.environment import env
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

name = "mySQL-shop"


def run():
    # Check if mySQL is already running
    result = subprocess.run(
        [
            "docker",
            "ps",
            "--filter",
            f"name={name}",
            "--filter",
            "status=running",
            "--format",
            "{{.Names}}",
        ],
        capture_output=True,
        text=True,
    )

    if name not in result.stdout:
        # Next we will run the mySQL instance and allow for the fact that docker may already have a container
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                f"name={name}",
                "--filter",
                "status=exited",
                "--format",
                "{{.Names}}",
            ],
            capture_output=True,
            text=True,
        )

        if name in result.stdout:
            print("Starting mySQL instance...")
            subprocess.run(["docker", "start", name], check=True)
            print("mySQL instance started.")

        else:
            subprocess.run(
                [
                    "docker",
                    "run",
                    "-d",
                    "--name",
                    name,
                    "-e",
                    f"MYSQL_ROOT_PASSWORD={env('DB_PASSWORD')}",
                    "-e",
                    f"MYSQL_DATABASE={env('DB_NAME')}",
                    "-p",
                    f"{env('DB_PORT')}:{env('DB_PORT')}",
                    "mysql:latest",
                ],
                check=True,
            )


def wait(mysqldb):
    # Wait for mySQL to start accepting connections from scripts
    max_attempts = 30

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} attempts"),
        transient=True,
    ) as progress:
        task = progress.add_task("Waiting for MySQL to start...", total=max_attempts)

        for _ in range(max_attempts):
            try:
                test_db = mysqldb.connect(
                    host=env("DB_HOST"),
                    user=env("DB_USER"),
                    password=env("DB_PASSWORD"),
                    port=int(env("DB_PORT")),
                )
                test_db.close()
                return
            except mysqldb.Error:
                time.sleep(2)
                progress.advance(task)

    raise Exception("MySQL failed to start after maximum attempts.")
