"""
Theme upgrade:
  1. static/css/style.css   -> light + dark theme variables, readable sidebar
  2. templates/base.html    -> adds theme toggle button + early theme script
  3. Verifies template tag balance automatically
Run:  python phase6b_theme.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STYLE_CSS = '''
/* =====================================================================
   Cloud Attendance - stylesheet
   Light (default) and dark themes via [data-bs-theme]
   ===================================================================== */

/* ===== Theme tokens - LIGHT (default) ===== */
:root {
  --sidebar-width: 260px;

  --sidebar-bg: #ffffff;
  --sidebar-border: #e2e8f0;
  --sidebar-text: #0f172a;        /* near-black sidebar text */
  --sidebar-muted: #475569;
  --sidebar-hover-bg: #eef2f7;
  --sidebar-hover-text: #0f172a;  /* hover stays dark = always readable */
  --sidebar-active-bg: #2563eb;
  --sidebar-active-text: #ffffff;
  --soon-bg: #e2e8f0;
  --soon-text: #475569;

  --topbar-bg: #ffffff;
  --topbar-border: #e2e8f0;
  --topbar-text: #0f172a;
  --page-bg: #f1f5f9;
}

/* ===== Theme tokens - DARK ===== */
[data-bs-theme="dark"] {
  --sidebar-bg: #0f172a;
  --sidebar-border: #1e293b;
  --sidebar-text: #e2e8f0;
  --sidebar-muted: #94a3b8;
  --sidebar-hover-bg: #1e293b;
  --sidebar-hover-text: #f8fafc;
  --sidebar-active-bg: #3b82f6;
  --sidebar-active-text: #ffffff;
  --soon-bg: #334155;
  --soon-text: #cbd5e1;

  --topbar-bg: #1e293b;
  --topbar-border: #334155;
  --topbar-text: #e2e8f0;
  --page-bg: #0b1220;
}

body { background: var(--page-bg); }

/* ===== Layout: sidebar + main ===== */
.app-layout { min-height: 100vh; }

@media (min-width: 992px) {
  .app-layout { display: flex; }
  .sidebar {
    width: var(--sidebar-width);
    flex-shrink: 0;
    position: sticky; top: 0;
    height: 100vh;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--sidebar-border);
  }
  .main-area { flex-grow: 1; min-width: 0; }
}

@media (max-width: 991.98px) {
  .sidebar {
    background: var(--sidebar-bg);
    border-right: 1px solid var(--sidebar-border);
  }
}

/* ===== Sidebar ===== */
.sidebar-brand {
  height: 60px;
  color: var(--sidebar-text);
  font-weight: 700;
  font-size: 1.05rem;
  display: flex; align-items: center;
  padding: 0 1.25rem;
  border-bottom: 1px solid var(--sidebar-border);
}
.sidebar .offcanvas-header {
  border-bottom: 1px solid var(--sidebar-border);
  color: var(--sidebar-text);
}

.sidebar .nav-link {
  color: var(--sidebar-text);
  border-radius: .5rem;
  padding: .55rem .85rem;
  font-size: .925rem;
  font-weight: 500;
}
.sidebar .nav-link i { font-size: 1.05rem; }
.sidebar .nav-link:hover {
  color: var(--sidebar-hover-text);
  background: var(--sidebar-hover-bg);
}
.sidebar .nav-link.active {
  color: var(--sidebar-active-text);
  background: var(--sidebar-active-bg);
}
.sidebar-footer {
  border-top: 1px solid var(--sidebar-border);
  color: var(--sidebar-muted);
}

.badge.soon {
  background: var(--soon-bg);
  color: var(--soon-text);
  font-size: .6rem;
  letter-spacing: .05em;
  text-transform: uppercase;
  vertical-align: middle;
}

/* ===== Topbar ===== */
.topbar {
  height: 60px;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--topbar-border);
  position: sticky; top: 0; z-index: 1020;
}
.topbar-title { color: var(--topbar-text); }

/* ===== Cards / tables ===== */
.card { border-radius: .75rem; }
.table thead th {
  font-size: .75rem;
  text-transform: uppercase;
  letter-spacing: .04em;
  border-bottom-width: 1px;
}

/* Dark-mode fixes for white utility classes used in dashboard markup */
[data-bs-theme="dark"] .bg-white { background-color: #1e293b !important; }
[data-bs-theme="dark"] .text-bg-light {
  background-color: #334155 !important;
  color: #e2e8f0 !important;
  border-color: #475569 !important;
}
[data-bs-theme="dark"] .btn-light {
  background-color: #334155;
  border-color: #475569;
  color: #e2e8f0;
}

/* ===== Dashboard stat cards ===== */
.stat-card { transition: transform .12s ease, box-shadow .12s ease; }
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 .5rem 1rem rgba(15, 23, 42, .12) !important;
}
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  flex-shrink: 0;
}

/* ===== Charts ===== */
.chart-container { position: relative; height: 260px; }

/* ===== Login page ===== */
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 55%, #38bdf8 100%);
}
.login-page .form-control { padding: .65rem .85rem; }
'''

BASE_HTML = '''
{% load static %}
{% load nav %}
<!DOCTYPE html>
<html lang="en" data-bs-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Cloud Attendance{% endblock %}</title>
  <script>
    /* Apply saved theme BEFORE first paint to avoid flashing */
    (function () {
      document.documentElement.setAttribute(
        "data-bs-theme", localStorage.getItem("theme") || "light"
      );
    })();
  </script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
  {% block extra_css %}{% endblock %}
</head>
<body>
{% if user.is_authenticated %}
<div class="app-layout">

  <aside class="sidebar offcanvas-lg offcanvas-start" tabindex="-1" id="appSidebar">
    <div class="offcanvas-header border-bottom d-lg-none">
      <span class="fw-bold"><i class="bi bi-mortarboard-fill text-primary me-2"></i>Cloud Attendance</span>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" data-bs-target="#appSidebar"></button>
    </div>
    <div class="offcanvas-body d-flex flex-column p-0">
      <div class="sidebar-brand d-none d-lg-flex">
        <i class="bi bi-mortarboard-fill me-2"></i> Cloud Attendance
      </div>
      <nav class="sidebar-nav flex-grow-1 overflow-auto px-2 py-2">
        <ul class="nav flex-column gap-1">
          {% nav_items as items %}
          {% for item in items %}
          <li>
            <a class="nav-link {{ item.active }}" href="{{ item.url }}">
              <i class="bi {{ item.icon }} me-2"></i>{{ item.label }}
              {% if item.soon %}<span class="badge soon">soon</span>{% endif %}
            </a>
          </li>
          {% endfor %}
        </ul>
      </nav>
      <div class="sidebar-footer small px-3 py-2">
        Signed in as <strong>{{ user.username }}</strong>
      </div>
    </div>
  </aside>

  <div class="main-area d-flex flex-column min-vh-100">
    <header class="topbar d-flex align-items-center gap-2 px-3">
      <button class="btn btn-outline-secondary btn-sm d-lg-none" data-bs-toggle="offcanvas" data-bs-target="#appSidebar" aria-controls="appSidebar">
        <i class="bi bi-list"></i>
      </button>
      <h1 class="topbar-title h6 mb-0">{% block page_title %}{% endblock %}</h1>
      <div class="ms-auto d-flex align-items-center gap-2">
        <button class="btn btn-outline-secondary btn-sm" id="themeToggle" type="button"
                title="Toggle dark / light theme" aria-label="Toggle theme">
          <i class="bi bi-moon-stars" id="themeIcon"></i>
        </button>
        <div class="dropdown">
          <button class="btn btn-light btn-sm dropdown-toggle d-flex align-items-center gap-2" data-bs-toggle="dropdown">
            <i class="bi bi-person-circle"></i>
            <span class="d-none d-sm-inline">{{ user.username }}</span>
            {% if user.is_admin_role %}<span class="badge text-bg-danger">Admin</span>{% elif user.is_teacher_role %}<span class="badge text-bg-primary">Teacher</span>{% else %}<span class="badge text-bg-success">Student</span>{% endif %}
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm">
            <li><a class="dropdown-item" href="{% nav_url 'profile' %}"><i class="bi bi-person me-2"></i>Profile</a></li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <form method="post" action="{% url 'logout' %}">
                {% csrf_token %}
                <button type="submit" class="dropdown-item text-danger"><i class="bi bi-box-arrow-right me-2"></i>Logout</button>
              </form>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <main class="content flex-grow-1 p-3 p-lg-4">
      {% if messages %}
        {% for message in messages %}
        <div class="alert {% if message.tags == 'error' %}alert-danger{% else %}alert-{{ message.tags|default:'info' }}{% endif %} alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}
      {% endif %}
      {% block content %}{% endblock %}
    </main>

    <footer class="text-center text-muted small py-3">
      Cloud-Based Student Attendance System - Computer Networks Microproject | Django + Supabase PostgreSQL
    </footer>
  </div>
</div>
{% else %}
<div class="container py-5">
  {% block anonymous_content %}{% endblock %}
</div>
{% endif %}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<script>
  /* Theme toggle - choice persists in localStorage */
  (function () {
    var btn = document.getElementById("themeToggle");
    var icon = document.getElementById("themeIcon");
    if (!btn) return;
    function paint(t) {
      icon.className = (t === "dark") ? "bi bi-sun" : "bi bi-moon-stars";
    }
    paint(document.documentElement.getAttribute("data-bs-theme"));
    btn.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-bs-theme", next);
      localStorage.setItem("theme", next);
      paint(next);
    });
  })();
</script>
{% block extra_js %}{% endblock %}
</body>
</html>
'''


def check_balance(text, name):
    openers = {"if": "endif", "for": "endfor", "block": "endblock", "with": "endwith"}
    mids = {"elif", "else"}
    stack, problems = [], []
    for lineno, line in enumerate(text.splitlines(), 1):
        for tag in re.findall(r"{%-?\s*(\w+)", line):
            if tag in openers:
                stack.append((tag, lineno))
            elif tag in openers.values():
                if not stack:
                    problems.append(f"{name}:{lineno} extra {{% {tag} %}}")
                elif openers[stack[-1][0]] != tag:
                    problems.append(f"{name}:{lineno} {{% {tag} %}} mismatches line {stack[-1][1]}")
                    stack.pop()
                else:
                    stack.pop()
            elif tag in mids and (not stack or stack[-1][0] != "if"):
                problems.append(f"{name}:{lineno} ORPHANED {{% {tag} %}}")
    for tag, lineno in stack:
        problems.append(f"{name}:{lineno} {{% {tag} %}} never closed")
    return problems


def main():
    css_path = ROOT / "static" / "css" / "style.css"
    base_path = ROOT / "templates" / "base.html"

    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(STYLE_CSS.strip() + "\n", encoding="utf-8")
    base_path.write_text(BASE_HTML.strip() + "\n", encoding="utf-8")

    print(f"Wrote {css_path.relative_to(ROOT)}  ({len(STYLE_CSS.strip().splitlines())} lines)")
    print(f"Wrote {base_path.relative_to(ROOT)}  ({len(BASE_HTML.strip().splitlines())} lines)")

    problems = check_balance(base_path.read_text(encoding="utf-8"), "base.html")
    print("\nALL CHECKS PASSED - base.html tags are balanced." if not problems
          else "\nPROBLEMS:\n" + "\n".join("  - " + p for p in problems))


if __name__ == "__main__":
    main()