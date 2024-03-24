import random
from database.credentials import get_genlayer_db_connection
import tarfile
import time
from io import BytesIO


def vrf(items, weights, k):
    weighted_indices = random.choices(range(len(items)), weights=weights, k=k * 10)
    unique_indices = set()
    random.shuffle(weighted_indices)

    for idx in weighted_indices:
        unique_indices.add(idx)
        if len(unique_indices) == k:
            break

    return [items[i] for i in unique_indices]


def get_contract_state(contract_address: str) -> dict: # that should be on the rpc and cli maybe
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT state FROM current_state WHERE id = %s;", (contract_address,)
        )
        contract_row = cursor.fetchone()

        if contract_row is not None:
            contract_state = contract_row[0]
            return contract_state
        else:
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def create_tar_archive(file_name, file_content):
    pw_tarstream = BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode="w")
    file_data = file_content.encode("utf-8")

    tarinfo = tarfile.TarInfo(name=file_name)
    tarinfo.size = len(file_data)
    tarinfo.mtime = time.time()

    pw_tar.addfile(tarinfo, BytesIO(file_data))
    pw_tar.close()
    pw_tarstream.seek(0)
    return pw_tarstream

def write_json_from_docker_tar(bits, path):
    file_like_object = BytesIO()
    for chunk in bits:
        file_like_object.write(chunk)
    file_like_object.seek(0)  # Rewind the file-like object to read from it

    with tarfile.open(fileobj=file_like_object) as tar:
        member = tar.next()  # Get the first member in the tar archive
        if member is not None:
            with open(path, "wb") as receipt_file:
                receipt_file.write(tar.extractfile(member).read())   