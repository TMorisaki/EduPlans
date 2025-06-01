from app.models.lesson_plan import LessonPlan
from app.models.user import User

from app.database import Base  # 必ず Base をここに import
# __init__.py で Base をインポートすることで、Alembic がモデルのメタデータを認識できるようにする