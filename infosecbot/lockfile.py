from fcntl import flock, LOCK_EX, LOCK_NB

class LockFile:
    lockfile_name = "lockfile"

    def __enter__(self):
        self.fd = open(self.lockfile_name, "w")
        flock(self.fd, LOCK_EX | LOCK_NB)
        return self

    def __exit__(self, type, value, traceback):
        self.fd.close()
