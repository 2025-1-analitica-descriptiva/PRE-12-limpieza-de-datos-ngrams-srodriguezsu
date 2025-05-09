import pandas as pd  # type: ignore


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""

    df = pd.read_csv(input_file)
    return df


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la
    columna 'text'"""

    df = df.copy()
    df["key"] = df["raw_text"]
    df["key"] = df["key"].str.strip()
    df["key"] = df["key"].str.lower()
    df["key"] = df["key"].str.replace("-", "")
    df["key"] = df["key"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    )
    df["key"] = df["key"].str.split()

    df["key"] = df["key"].str.join("")
    df["key"] = df["key"].map(
        lambda x: [x[t : t + n] for t in range(len(x))],
    )
    df["key"] = df["key"].apply(lambda x: sorted(set(x)))
    df["key"] = df["key"].str.join("")

    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    #
    # Este código es identico al anteior
    #
    keys = df.copy()
    keys = keys.sort_values(by=["key", "raw_text"], ascending=[True, True])
    keys = keys.drop_duplicates(subset="key", keep="first")
    key_dict = dict(zip(keys["key"], keys["raw_text"]))
    df["cleaned_text"] = df["key"].map(key_dict)

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""
    #
    # Este código es identico al anteior
    #
    df = df.copy()
    df = df[["raw_text", "cleaned_text"]]
    df.to_csv(output_file, index=False)


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""
    #
    # Este código es identico al anteior
    #
    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("files/test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="files/input.txt",
        output_file="files/output.txt",
    )