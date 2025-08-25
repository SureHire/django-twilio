from django.utils.encoding import force_str, smart_str  # re-export

try:
    from django.utils.translation import gettext as _
    from django.utils.translation import gettext_lazy as _lazy
except Exception:  # pragma: no cover
    from django.utils.translation import ugettext as _  # type: ignore
    from django.utils.translation import ugettext_lazy as _lazy  # type: ignore

__all__ = ["force_str", "smart_str", "_", "_lazy"]
