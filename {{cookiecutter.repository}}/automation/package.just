# Define package tasks workflow to run when running 'just package'
[group('package')]
package: package-build

# Create snapshot of package constraints
[group('package')]
package-constraints constraints="constraints.txt":
	{% raw %}uv pip compile pyproject.toml --generate-hashes --output-file={{constraints}}{% endraw %}

# Build package based on constraint snapshot, removes previous builds when available
[group('package')]
package-build constraints="constraints.txt": remove-build package-constraints
	{% raw %}uv build --build-constraint={{constraints}} --require-hashes --wheel{% endraw %}
