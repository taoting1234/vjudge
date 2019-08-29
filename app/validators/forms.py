from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import NotFound
from app.models.language import Language
from app.models.problem import Problem
from app.models.solution import Solution
from app.models.user import User
from app.validators.base import BaseForm as Form


class UsernameForm(Form):
    username = StringField(validators=[DataRequired()])

    def validate_username(self, value):
        user = User.get_by_id(self.username.data)
        if not user:
            raise NotFound('The user does not exist')


class PasswordForm(Form):
    password = StringField(validators=[DataRequired()])


class LoginForm(UsernameForm, PasswordForm):
    pass


class RegisterForm(PasswordForm):
    username = StringField(validators=[DataRequired()])

    def validate_username(self, value):
        user = User.get_user_by_username(self.username.data)
        if user:
            raise NotFound('The user already exist')


class CodeForm(Form):
    code = StringField(validators=[DataRequired()])


class UserInfoForm(Form):
    gender = IntegerField(validators=[DataRequired()])
    college = StringField(validators=[DataRequired()])
    profession = StringField(validators=[DataRequired()])
    class_ = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    qq = StringField(validators=[DataRequired()])
    remark = StringField()


class PageForm(Form):
    page = IntegerField()
    page_size = IntegerField()

    def validate_page(self, value):
        if self.page.data:
            if self.page.data <= 0:
                raise ValidationError('Page must >= 1')
        else:
            self.page.data = 1

    def validate_page_size(self, value):
        if self.page_size.data:
            if self.page_size.data > 100:
                raise ValidationError('Page size must <= 100')
        else:
            self.page_size.data = 20


class SearchUserForm(PageForm):
    nickname = StringField()
    gender = StringField()
    college = StringField()
    profession = StringField()
    class_ = StringField()
    phone = StringField()
    qq = StringField()
    permission = IntegerField()
    remark = StringField()


class CreateSolutionForm(Form):
    problem_id = IntegerField(validators=[DataRequired()])
    language = StringField(validators=[DataRequired()])
    code = StringField(validators=[DataRequired()])

    def validate_language(self, value):
        problem = Problem.get_by_id(self.problem_id.data)
        if not problem:
            raise ValidationError('The problem does not exist')
        res = Language.search(oj=problem.remote_oj, key=self.language.data)
        if res['count'] == 0:
            raise ValidationError('The language does not exist')


class SubmitCaptchaForm(Form):
    solution_id = IntegerField(validators=[DataRequired()])
    captcha = StringField(validators=[DataRequired()])

    def validate_solution_id(self, value):
        solution = Solution.get_by_id(self.solution_id.data)
        if not solution:
            raise ValidationError('The solution does not exist')
        if solution.remote_id:
            raise ValidationError('The solution was submitted')
