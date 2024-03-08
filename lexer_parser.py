import re

class YALexLexer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []

    def tokenize(self):
        with open(self.filename, 'r') as file:
            content = file.read()

            # Dividir el contenido en secciones
            sections = self._split_sections(content)

            # Analizar cada sección
            for section in sections:
                self._parse_section(section)

    def _split_sections(self, content):
        # Dividir el contenido en secciones basadas en {header}, {entrypoint}, {trailer}, etc.
        # Utilizamos expresiones regulares para esto
        return re.split(r'\n\s*{(?:header|trailer|rule)}\s*\n', content)

    def _parse_section(self, section):
        # Analizar una sección específica del archivo YALex
        # Dividimos la sección en líneas y eliminamos las líneas en blanco
        lines = [line.strip() for line in section.split('\n') if line.strip()]

        if lines:
            # La primera línea define el nombre del token
            token_name = lines[0]

            # Las líneas restantes contienen expresiones regulares y acciones
            for line in lines[1:]:
                # Ignorar líneas que contienen comentarios de tipo (* *)
                if '(*' in line and '*)' in line:
                    continue

                # Dividir la línea en expresión regular y acción (si existe)
                parts = line.split('{', 1)
                regexp = parts[0].strip()
                action = parts[1].split('}')[0].strip() if len(parts) > 1 else None

                # Agregar el token analizado a la lista
                self.tokens.append((token_name, regexp, action))

    def display_tokens(self):
        for token in self.tokens:
            print("Token:", token[0])
            print("Regular Expression:", token[1])
            print("Action:", token[2])
            print()

# Ejemplo de uso
lexer = YALexLexer('lexer.yal')
lexer.tokenize()
lexer.display_tokens()
