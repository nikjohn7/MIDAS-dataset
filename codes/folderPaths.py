from pathlib import Path
#
class Folders:
    def __init__(self, rootDir, inputDir):
        self.root = rootDir
        self.input = inputDir

    def ensureFolder(self, dir):
        mediadir = Path(dir)
        mediadir.mkdir(parents=True, exist_ok=True)

    def getDatasetFolder(self):
        d = Path(self.root) / self.input
        return str(d)

    def getGoogleResultsRoot(self, ensureDir=True):
        d =  Path(self.root) / 'results' / self.input
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

    def getContentRoot(self, ensureDir=True):
        d =  Path(self.root) / 'content' / self.input
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

    def getMatchesRoot(self, ensureDir=True):
        d =  Path(self.root) / 'matches' / self.input
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

    def getImagesRoot(self, ensureDir=True):
        d =  Path(self.root) / 'images' / self.input
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

    def getFolder(self, folderName, ensureDir=True):
        d = Path(self.root) / folderName / self.input
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

    def getUnmatchedRoot(self, ensureDir=True):
        d = Path(self.getMatchesRoot(ensureDir)) / 'unmatched'
        if ensureDir:
            self.ensureFolder(d)
        return str(d)

