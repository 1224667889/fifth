from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class RoomForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField(label=u'昵称',
                       validators=[DataRequired()],
                       render_kw={

                       })
    room = StringField(label=u'房间名称', validators=[DataRequired()])
    submit = SubmitField(label=u'进入房间')