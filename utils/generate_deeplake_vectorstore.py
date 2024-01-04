from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pathlib import Path
import argparse
load_dotenv()


def convert_to_deeplake_vdb(args):
    filepath = Path(args.csv_file)
    filename = filepath.stem

    dataset_path = f"./{args.dataset_output_dir}/{filename}"

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    db = DeepLake(dataset_path=dataset_path, embedding=embeddings, num_workers=4)

    if len(db.vectorstore) == 0:
        with open(filepath, encoding= 'utf-8') as f:
            text_data = f.read()

        # we split the documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=args.chunk_size, chunk_overlap=0, length_function=len,)
        docs = text_splitter.split_text(text_data)

        # add documents to our Deep Lake dataset
        db.add_texts(docs[:args.max_docs_length])
    else:
        print("Dataset is not empty.")

def get_parsers():
    parser = argparse.ArgumentParser(description='Convert csv to Deep Lake VectorDB.')
    parser.add_argument('--dataset_output_dir', type=str, default='deeplake/',
                        help='Dataset output directory.')
    parser.add_argument('--csv_file', required=True,
                        help='Path to csv file.')
    parser.add_argument('--chunk_size', type=int, default=350,
                        help="Text splitter chunk size.")
    parser.add_argument('--max_docs_length', type=int, default=20000,
                        help="Maximum number data to store after chuncking in datalake.")

    return parser.parse_args()

if __name__ == '__main__':
    args = get_parsers()
    convert_to_deeplake_vdb(args)