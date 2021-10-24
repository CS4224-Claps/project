from utils.connection import connection
from utils.setup import setup


def main():
    session = connection()
    setup(session, './schema/schema.cql', '../../seed/data_files')    

    session.shutdown()

if __name__ == "__main__":
    main()

