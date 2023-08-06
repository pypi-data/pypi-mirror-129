class AbstractState():
    """状態"""

    def __init__(self):
        pass

    def entry(self, context):
        """この状態に遷移したときに呼び出されます

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
        self.on_entry(context)
        return None

    def on_entry(self, context):
        """この状態に遷移したときに呼び出されます

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です
        """
        pass

    def exit(self, context, line, edge_path):
        """この状態から抜け出たときに呼び出されます。ただし初期化時、アボート時は呼び出されません

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です。 Defaults to None.
        line : str
            コマンドライン文字列
        edge_path : list
            辺パス

        Parameters
        ----------
        context : Context
            このステートマシンは、このContextが何なのか知りません。
            外部から任意に与えることができる変数です

        Returns
        -------
        str
            次（下位）の辺の名前
        """
        self.on_exit(context)

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
