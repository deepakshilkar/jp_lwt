from reader import reader

@reader.route('/')
@reader.route('/index')
def index():
    return "Hello, World!"
