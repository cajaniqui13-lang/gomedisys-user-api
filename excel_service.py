import pandas as pd


class ExcelService:
    @staticmethod
    def read_documentos_file(file_path: str):
        df = pd.read_excel(file_path)

        # Mapeo de nombres para tolerar tildes, mayúsculas o variaciones
        column_mapping = {}
        for col in df.columns:
            col_str = str(col).strip().lower()
            if col_str in [
                "documento",
                "numero de documento",
                "número de documento",
                "cedula",
                "cédula",
                "documento de identidad",
                "cc",
            ]:
                column_mapping[col] = "Documento"

        df = df.rename(columns=column_mapping)

        # Validación
        if "Documento" not in df.columns:
            raise ValueError(
                "Falta la columna obligatoria 'Documento' en el archivo Excel."
            )

        # Limpieza — evita que pandas convierta el documento a notación
        # científica o le agregue decimales (".0") si la columna es numérica.
        def limpiar_documento(valor):
            if pd.isna(valor):
                return ""
            if isinstance(valor, float) and valor.is_integer():
                return str(int(valor))
            return str(valor).strip()

        df["Documento"] = df["Documento"].apply(limpiar_documento)

        # Descartar filas vacías
        df = df[df["Documento"] != ""]

        if df.empty:
            raise ValueError(
                "El archivo Excel no tiene filas válidas con la columna Documento."
            )

        return df.to_dict(orient="records")
