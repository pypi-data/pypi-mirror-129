class AbstractState():
    """状態"""

    def __init__(self):
        pass

    def on_entry(self, context):
        """この状態に遷移したときに呼び出されます

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です
        """
        pass

    def pass_on(self, context):
        """この状態に遷移したあと、ただちに次の状態へ遷移したいときに記述してください

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です

        Returns
        -------
        object
            ただちに state_machine.leave(...) に渡す引数です。
            None を指定すると、たたちに次の状態に遷移することはしません
        """
        return None

    def on_exit(self, context):
        """この状態から抜け出たときに呼び出されます。ただし初期化時、アボート時は呼び出されません

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です
        """
        pass
