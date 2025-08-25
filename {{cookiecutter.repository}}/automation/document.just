# Use pdoc to create package documentation
[group('document')]
doc-build format="google" output="docs": clean-docs
    {% raw %}uv run pdoc --docformat={{format}} --output-directory={{output}} {{SOURCES}}/{{PACKAGE}}{% endraw %}

# Show documentation on local host
[group('document')]
doc-serve format="google" port="8088":
    {% raw %}uv run pdoc --docformat={{format}} --port={{port}} {{SOURCES}}/{{PACKAGE}}{% endraw %}
