# Define package tasks workflow to run when running 'just package'
[group('package')]
package: package-build

# Create snapshot of package constraints
[group('package')]
package-constraints constraints="constraints.txt":
	uv pip compile pyproject.toml --generate-hashes --output-file={{constraints}}

# Build package based on constraint snapshot, removes previous builds when available
[group('package')]
package-build constraints="constraints.txt": remove-build package-constraints
	uv build --build-constraint={{constraints}} --require-hashes --wheel

[group('package')]
package-run-dev:
	uvx --from dist/*.whl ecommerce config/dev.yml

[group('package')]
package-run-prod:
	uvx --from dist/*.whl ecommerce config/prod.yml
