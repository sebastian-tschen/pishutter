from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/shutter/")
def add_something():
    return """
    <html><head>    <link rel="stylesheet" href="../static/style.css"></head><body>
    <!-- ######## This is a comment, visible only in the source editor  ######## --><form><input name="name" type="text" value="Frank" /> <br /> <input name="democheckbox" type="checkbox" value="1" /> Checkbox<br /> <button type="submit" value="Submit">Submit</button></form><form accept-charset="UTF-8" action="action_page.php" autocomplete="off" method="GET" target="_blank"><fieldset><legend>Title:</legend> <label for="name">Name</label><br /> <input name="name" type="text" value="Frank" /> <br /> <input checked="checked" name="sex" type="radio" value="male" /> Male <br /> <input name="sex" type="radio" value="female" /> Female <br /> <textarea cols="30" rows="2">Long text.</textarea><br /><select>
<option selected="selected" value="1">Yes</option>
<option value="2">No</option>
</select><br /> <input name="democheckbox" type="checkbox" value="1" /> Checkbox<br /> <button type="submit" value="Submit">Submit</button></fieldset></form>
</body>
</html>
"""


