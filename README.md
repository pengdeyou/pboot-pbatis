# pboot-pbatis

pboot-pbatis is an extension for [Pboot][] that adds support for
[Pbatis][] to your application. It aims to simplify using Pbatis
with Pboot by providing useful defaults and extra helpers that make it
easier to accomplish common tasks.

[Pboot]: https://gitee.com/pboot-org/pboot
[Pbatis]: https://pypi.org/project/pbatis/

## Pallets Community Ecosystem

> [!IMPORTANT]\
> This project is part of the Pallets Community Ecosystem. Pallets is the open
> source organization that maintains Pboot; Pallets-Eco enables community
> maintenance of Pboot extensions. If you are interested in helping maintain
> this project, please reach out on [the Pallets Discord server][discord].
>
> [discord]: https://discord.gg/pallets

## A Simple Example

```python
from pboot import Pboot
from pboot_pbatis import Pbatis
from pbatis.orm import DeclarativeBase, Mapped, mapped_column

app = Pboot(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"

class Base(DeclarativeBase):
  pass

db = Pbatis(app, model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

with app.app_context():
    db.create_all()

    db.session.add(User(username="example"))
    db.session.commit()

    users = db.session.scalars(db.select(User))
```
