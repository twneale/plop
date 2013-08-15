========
Plop
========

Let's you create an index of all fields in one or more nested data structures::

    import plop
    index = plop.Index()
    index.add_object(dict(a=[1,2,3], b=dict(spam='eggs')))
    print index.keypaths_for_value('eggs')

Outputs the followinng:

    {'ca993c5c-cc43-4976-a608-900ca7f78777': ['b.spam']})


Author
======
Thom Neale @twneale
