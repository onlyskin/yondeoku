import json
from yondeoku.polish.Token import Token
from yondeoku.polish.Block import Block
from yondeoku.polish.User import User
from yondeoku.japanese.jBlock import jBlock
from yondeoku.japanese.Sentence import Sentence

class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Token):
            return {
                "tokenText": obj.tokenText,
                "strippedText": obj.strippedText,
                "startIndex": obj.startIndex,
                "strippedStartIndex": obj.strippedStartIndex}
        if isinstance(obj, Block):
            return {
                "type": "Block",
                "text": obj.text,
                "tokens": obj.tokens,
                "lemmaList": obj.lemmaList,
                "bestLemmaList": obj.bestLemmaList,
                "readTokens": obj.readTokens
            }
        if isinstance(obj, User):
            return {
                "username": obj.username,
                "Blocks": obj.Blocks,
                "pickleFilePath": obj.pickleFilePath,
                "known": obj.known,
                "jKnown": obj.jKnown,
                "threshold": obj.threshold
            }
        if isinstance(obj, jBlock):
            return {
                "type": "jBlock",
                "jText": obj.jText,
                "sentences": obj.sentences,
                "readSentences": obj.readSentences
            }
        if isinstance(obj, Sentence):
            return {
                "index": obj.index,
                "length": obj.length,
                "text": obj.text,
                "tokens": obj.tokens
            }
        if isinstance(obj, set):
            return list(obj)
        return super(UserEncoder, self).default(obj)
