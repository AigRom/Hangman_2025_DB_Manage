from controllers.Controller import Controller
from models.Model import Model
from views.View import View



if __name__ == '__main__':
    model = Model()
    view = View(model)
    Controller(model, view)

    view.mainloop() # Koodi "viimane" rida