from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4


def create_pdf(filename, budgets):
    w, h = A4
    canvas = Canvas('/tmp/' + filename, pagesize=A4)
    canvas.setFont('Helvetica', 14)
    textobject = canvas.beginText(50, h - 50)
    textobject.textLine('Creado el: ' + filename.replace('pdf', ''))
    textobject.moveCursor(125, 10)
    textobject.textLine('Presupuesto de Tratamientos EDENT')
    textobject.moveCursor(-75, 100)
    for budget in budgets:
        textobject.textLine(budget['name'] + ' : Q' + budget['price'])
        textobject.moveCursor(0, 15)
    textobject.moveCursor(250, 30)
    textobject.textLine('Total: Q' + str(get_total(budgets)))
    canvas.drawText(textobject)
    canvas.save()


def get_total(budgets):
    total = 0
    for budget in budgets:
        total += int(budget['price'])
    return total
