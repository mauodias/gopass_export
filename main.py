import click

import functions

# def process_old(
#     path: str, secrets: List[str], passphrase: str, key_file: str
# ) -> Tuple[Dict[str, Dict[str, Sequence[str]]], List[str], List[str], List[str]]:
#     processed = {}
#     complex = []
#     multiline = []
#     failed = []
#     for secret in secrets:
#         secret_path = secret
#         secret = secret.replace(f"{path}/", "")
#         elements = secret.split("/")
#         if len(elements) > 2:
#             complex.append(secret_path)
#             continue
#         name = elements[0]
#         user = elements[1].replace(".gpg", "")
#         try:
#             contents = decrypt(key_file, passphrase, secret_path).split("\n")
#         except PGPError:
#             failed.append(secret_path)
#             continue
#         if len(contents) > 1:
#             multiline.append(secret_path)
#             continue
#         processed[name] = {"user": user, "contents": contents}
#     return processed, complex, multiline, failed


@click.command()
@click.option("--path", default=".", help="Path to secrets", show_default=True)
@click.option("--key-file", default="~/.gnupg/secring.gpg", help="Path to key file", show_default=True)
@click.option(
    "--passphrase",
    prompt="Enter your key file password",
    help="Passphrase for key file",
    hide_input=True,
)
@click.option("--interactive", is_flag=True, default=False, help="Interactive mode")
def main(path: str, key_file: str, passphrase: str, interactive: bool) -> None:
    secret_files = functions.find_encrypted_files(path)
    secrets = []
    for secret_file in secret_files:
        try:
            contents = functions.decrypt_file(key_file, passphrase, secret_file)
        except:
            print(f"Failed to decrypt {secret_file}")
            continue
        secret = functions.create_secret(path, secret_file, contents)
        if interactive:
            print(secret)
            if click.confirm("Is this correct?"):
                secrets.append(secret)
        else:
            secrets.append(secret)


if __name__ == "__main__":
    main()
