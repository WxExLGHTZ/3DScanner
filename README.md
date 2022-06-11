# Fachuebergreifendes Projekt: 3D-Scanner mit einer Intel RealSense

Ziel des Projektes ist es ein Produkt zu schaffen mit dem jeder Interessierte die Option hat diverse Objekte zu digitalisieren.
Es soll die Möglichkeit geboten werden die Objekte zu scannen und daraus 3D – Modelle zu erstellen.

## Authoren

- Teammitglieder:
  1. Vinh Thong Trinh
  2. Mert Karadeniz
  3. Habib Ben Khedher
  4. William Eppel
- Team: 3
- Semester: SS22

### Technologiestack:

- Python 3.8.x
- PyQt5

### Voraussetzungen + Installation:

**Python Installation**

1. Installieren Sie [Python3.8](https://www.python.org/downloads/release/python-380/) den Windows x86-64 executable installer

2. Nach der Installation im Pfad "03-3dscanner\Software" eine eigene virtuelle Umgebung anlegen. Öffne anschließend die Kommandozeile als Adminstrator und navigiere zu oben genannten Pfad.

```cmd
>  cd 03-3dscanner\Software
```

3. Geben Sie anschließend folgendes ein:

```cmd
>  {path to python.exe} -m venv venv
```

Es muss der komplette Pfad der Python.exe ohne Klammern angegeben werden!

4. Virtuelle Umgebung aktivieren und pip upgraden/installieren

```cmd
> .\venv\Scripts\activate
(venv) > python -m pip install --upgrade pip
```

5. Alle nötigen packages installieren

```cmd
(venv) > pip install -r requirements.txt
```

## Hinweise

- Legen Sie Ihre Daten zwingend in die jeweiligen Unterordner ab!
- Fügen Sie am Ende in das `README.md` Installationshinweise und Hinweise für das Setup Ihres Projektergebnisses ein!
- Sie können unterschiedliche Branches verwenden, Ergebnisse und Abgaben müssen aber im Master-Branch eingecheckt werden.
