Context
    Context stores temporary data during a request.
    Flask provides global objects:
        request → user input
        session › user data
        g → temporary global data

Why important?
    Access request data easily
    Maintain user state
Example:
    request.form['username']
    