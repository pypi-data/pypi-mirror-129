# pylogz
 Super basic logger used in personal projects.

---

Why should you use this? You probably shouldn't.

---

## Quickstart

```bash
pip install --upgrade pylogz
```

## Usage

```python
from logz import get_logger 

logger = get_logger(name='libname', log_level='info', *args, **kwargs)
logger.info('...')

### Multi lib usage, threadsafe-ish

from logz import get_cls_logger
get_logger = get_cls_logger(name='libname', log_level='info', *args, **kwargs)

# Now you can call the get_logger function from any submodule.

```