pre-commit-hooks
================

Some custom hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/jheerman/license-checker
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    -   id: license-checker
```

### Hooks available

#### `license-checker`
Checks for the existence of license keys.
