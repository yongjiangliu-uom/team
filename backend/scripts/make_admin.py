import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from ewastehub import create_app  # noqa: E402
from ewastehub.extensions import db  # noqa: E402
from ewastehub.models import User  # noqa: E402


#   python scripts/make_admin.py test1@example.com
def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/make_admin.py <email>")
        raise SystemExit(1)

    email = sys.argv[1].strip().lower()

    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found:", email)
            raise SystemExit(1)

        user.role = "admin"
        db.session.commit()
        print("OK, set admin:", email)


if __name__ == "__main__":
    main()