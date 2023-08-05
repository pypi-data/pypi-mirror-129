# TSRU (TSR Utils)

A python library for doing various miscellaneous things

## Features

### **tsru.printing**

- **LoadingSpinner**

    Shows a spinner in the console while you can do something else in the background.
    Has support for custom loading, done and failed messages. It comes with in-build colorama support for the default values.  
    Example:  

    ```py
    from tsru.printing import LoadingSpinner
    import time

    spinner = LoadingSpinner("Running message", "Done msg", "Failed msg") 
    time.sleep(1)
    spinner.stop() # We are successfully done

    spinner = LoadingSpinner("Running message", "Done msg", "Failed msg")
    time.sleep(1)
    spinner.stop(False) # Something failed
    ```

    >/ Running message  
    >\ Running message  
    >\- Running message  
    >/ Running message  
    >Done msg Running message  
    >/ Running message  
    >\ Running message  
    >\- Running message  
    >/ Running message  
    >Failed msg Running message
