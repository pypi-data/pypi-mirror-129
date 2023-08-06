# fur-validation

## About
Fur validation is a package to help on validation/authorization of event based messages
using uuidv5 namespace secret.

It manages to create different keys each time, but those keys, are based on a static secret. Hense, it makes the authentication secure by not using the same keys each time. 