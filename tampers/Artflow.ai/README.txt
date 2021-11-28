SAVE: will attempt to save the six images you've created to desktop. Make sure popups are not blocked.
BATCH: Will enqueue up to 6 images sequentially from the large (square) input area under the main one,
removing them from the aformentioned input area. This behavior can be toggled by the 'Do Not Overwrite' tick-box.
Images can also have multiplicities of the form:

decimal*prompt

Wherein the batch button will attempt to enqueue max(6,decimal) entries of 'prompt', in-order. This persists across
calls as well, for example '8*girl' will queue 6 'girl' on the first batch, and then 2 on the second, followed by the
next four it is able to pull from the input square.