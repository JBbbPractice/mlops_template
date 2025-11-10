# Use pdoc to create package documentation
[group('document')]
doc-build format="google" output="docs":
    uv run pdoc --docformat={{format}} --output-directory={{output}} {{SOURCES}}/{{PACKAGE}}

# Show documentation on local host
[group('document')]
doc-serve format="google" port="8088":
    uv run pdoc --docformat={{format}} --port={{port}} {{SOURCES}}/{{PACKAGE}}
