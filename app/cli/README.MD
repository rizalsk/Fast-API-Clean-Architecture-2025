# FastAPI Extended Artisan-Style CLI

This CLI provides artisan-style commands for FastAPI projects, such as creating models, migrations, modules, and running database seeds.

---

## Available CLI Commands

### Make Commands

| Command                           | Description             |
| --------------------------------- | ----------------------- |
| `make:model <model_name>`         | Create a new model.     |
| `make:migration <migration_name>` | Create a new migration. |
| `make:module <module_name>`       | Create a new module.    |

### Database Commands

| Command   | Description           |
| --------- | --------------------- |
| `db:seed` | Run database seeding. |

---

## How to Run

Run the CLI using:

```bash
fastapi make:model User
```

```bash
fastapi db:seed
```
