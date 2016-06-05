import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


txt = urwid.Text(u"Bo.gg", align='center')
fill = urwid.Filler(txt, 'top')

class ActionButton(urwid.Button):
    def __init__(self, caption, callback):
        super(ActionButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
            None, focus_map='reversed')

class Question(urwid.WidgetWrap):
    def __init__(self, name, choices=[]):
        super(Question, self).__init__(
            ActionButton([u" > next"], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", name, "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)

flow = [Question('Name?', [Question('Ben?')]), Question('Dob?')]

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            u"Nice to meet you,\n%s.\n\nPress Q to exit." %
            edit.edit_text)

class ChoiceBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            u"Nice to meet you,\n%s.\n\nPress Q to exit." %
            edit.edit_text)




class Registration(object):
    def __init__(self):
        self.log = urwid.SimpleFocusListWalker([])
        self.top = urwid.ListBox(self.log)
        self.payload = {
            'username': None,
            'email': None,
            'password': None,
            'daily_weight_goal': None,
            'height': None,
            'weight': None,
            'activity_factor': None,
            'bogger': {
                'gender': None,
                'birthdate': None,
                'auto_update_goal': True,
            }
        }
        self.step = None
        self.set_step(flow[0])

    def set_step(self, step):
        if self.log:
            self.log[-1] = urwid.WidgetDisable(self.log[-1])
        self.log.append(QuestionBox(urwid.Edit('Name?')))
        self.log.append(QuestionBox(urwid.Edit('Name?')))
        self.log.append(QuestionBox(urwid.Edit('Name?')))
        self.log.append(QuestionBox(urwid.Edit('Name?')))
        self.top.focus_position = len(self.log) - 1
        self.step = step



flow = [
    QuestionBox('Name? '),
    QuestionBox('DOB? '),
]

def pop_question():
    for item in flow:
        yield item

class QuestionBox(urwid.Edit):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)

        log.append(pop_question())
        top.focus_position += 1

# edit = urwid.Edit(u"What is your name?\n")
# fill = QuestionBox(edit)
# loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
# loop.run()
#
# registration = Registration()

log = urwid.SimpleFocusListWalker([])
top = urwid.ListBox(log)
flow_index = 0
log.append(flow[flow_index])

import urwid

class PasswordEdit(urwid.Edit):
    def __init__(self, prompt):
        super(urwid.Edit, self).__init__(prompt)


activity_group = []
activity_buttons = [
    urwid.RadioButton(activity_group, 'Sedentary', state=False),
    urwid.RadioButton(activity_group, 'Lightly Active', state=False),
    urwid.RadioButton(activity_group, 'Moderately Active', state=False),
    urwid.RadioButton(activity_group, 'Very Active', state=False),
    urwid.RadioButton(activity_group, 'Extra Active', state=False),
]
gender_group = []
gender_buttons = [
    urwid.RadioButton(gender_group, 'Male', state=False),
    urwid.RadioButton(gender_group, 'Female', state=False),
]


flow = [
    urwid.Pile([urwid.Edit('Choose a username:\n')]),
    urwid.Pile([urwid.Edit('Enter your email:\n')]),
    urwid.Pile([urwid.Edit('Choose a password:\n', mask=u'*')]),
    urwid.Pile([urwid.Edit('Confirm password:\n', mask=u'*')]),
    urwid.Pile([urwid.Edit('How many pounds do you want to lose per week? (Usually between 0.5 and 2.0):\n')]),
    urwid.Pile([
        urwid.Text('The following questions are only used to calculate your basic metabolic rate and figure out ' \
               'how many calories you should be eating per day.\n'),
        urwid.Text('Activity Level (https://en.wikipedia.org/wiki/Physical_activity_level):\n'),
    ] + activity_buttons + [urwid.Text('')]),
    urwid.Pile([
        urwid.Text('Gender:\n'),
    ] + gender_buttons + [urwid.Text('')]),
    urwid.Pile([urwid.Edit('Birthdate (YYYY-MM-DD):\n')]),
    urwid.Pile([urwid.Edit('Enter your height (in inches):\n')]),
    urwid.Pile([urwid.Edit('Enter your weight (in pounds):\n')]),
]

flow_index = 0

class ConversationListBox(urwid.ListBox):
    def __init__(self):
        self.flow_index = 0
        body = urwid.SimpleFocusListWalker([flow[flow_index]])
        super(ConversationListBox, self).__init__(body)

    def keypress(self, size, key):
        key = super(ConversationListBox, self).keypress(size, key)
        if key != 'enter':
            return key
        name = self.focus[0].edit_text
        if not name:
            raise urwid.ExitMainLoop()
        # replace or add response
        # self.focus.contents[1:] = [(answer(name), self.focus.options())]
        # add a new question
        if self.focus_position == self.flow_index:
            self.next_question()
        else:
            self.focus_position += 1

    def next_question(self, data=None):
        pos = self.focus_position
        self.body.insert(pos + 1, flow[pos + 1])
        self.focus_position = pos + 1
        self.flow_index += 1

    def radio_callback(self, radio_button, new_state):
        self.next_question()

palette = [('prompt', 'default,bold', 'default'),]
conversation = ConversationListBox()
for button in activity_buttons + gender_buttons:
    urwid.connect_signal(button, 'change', conversation.radio_callback)

urwid.MainLoop(conversation, palette).run()
