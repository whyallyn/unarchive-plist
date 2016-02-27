Unarchive Plist
===============
This tool converts a property list (plist) file archived in the NSKeyedArchiver format to a serialized key-value paired plist for easier analysis.

About
-----
Property list (plist) files are a key source of forensic information on OS X and iOS systems. When viewing plist files that have been archived in the NSKeyedArchiver format, it's [extremely difficult](http://www.mac4n6.com/blog/2016/1/1/manual-analysis-of-nskeyedarchiver-formatted-plist-files-a-review-of-the-new-os-x-1011-recent-items) to quickly gain context around the values stored in the plist. `unarchive_plist.py` was created to better facilitate investigation of these archived files by allowing for quick conversion to a serialized plist file with basic key-value pairs. Much easier for your viewing pleasure!

**Before:**

```
"$objects" => [
  0 => "$null"
  1 => {
    "NS.keys" => [
      0 => <CFKeyedArchiverUID 0x7f807840ed70 [0x7fff72f38440]>{value = 2}
      1 => <CFKeyedArchiverUID 0x7f807840ed90 [0x7fff72f38440]>{value = 3}
      2 => <CFKeyedArchiverUID 0x7f807840edb0 [0x7fff72f38440]>{value = 4}
    ]
    "NS.objects" => [
      0 => <CFKeyedArchiverUID 0x7f807840ee20 [0x7fff72f38440]>{value = 5}
      1 => <CFKeyedArchiverUID 0x7f807840ee40 [0x7fff72f38440]>{value = 6}
      2 => <CFKeyedArchiverUID 0x7f807840ee60 [0x7fff72f38440]>{value = 10}
    ]
    "$class" => <CFKeyedArchiverUID 0x7f807840eed0 [0x7fff72f38440]>{value = 9}
  }
  2 => "version"
  3 => "properties"
  4 => "items"
  5 => 1
  6 => {
    "NS.keys" => [
      0 => <CFKeyedArchiverUID 0x7f807840ef70 [0x7fff72f38440]>{value = 7}
    ]
    "NS.objects" => [
      0 => <CFKeyedArchiverUID 0x7f807840efd0 [0x7fff72f38440]>{value = 8}
    ]
    "$class" => <CFKeyedArchiverUID 0x7f807840eed0 [0x7fff72f38440]>{value = 9}
  }
  7 => "com.apple.LSSharedFileList.MaxAmount"
  8 => 10
  9 => {
    "$classname" => "NSDictionary"
    "$classes" => [
      0 => "NSDictionary"
      1 => "NSObject"
    ]
  }
  <snip>
```

**After:**

```
"items" => [
    0 => {
      "bookmark" => <626f6f6b d4020000 ...>
      "properties" => {
      }
      "uniqueIdentifier" => "73F29D76-0446-4322-9A03-0C4F8557AE6C"
      "name" => "Calculator.app"
    }
    1 => {
      "bookmark" => <626f6f6b cc020000 ...>
      "properties" => {
      }
      "uniqueIdentifier" => "98EFAD5E-0BDE-4A25-A735-8C39E9600A82"
      "name" => "Safari.app"
    }
    2 => {
      "bookmark" => <626f6f6b 00040000 ...>
      "properties" => {
      }
      "uniqueIdentifier" => "1B3ECD35-1575-41A7-B797-9843C11520DD"
      "name" => "Signal Private Messenger.app"
    }
    3 => {
      "bookmark" => <626f6f6b d0020000 ...>
      "properties" => {
      }
      "uniqueIdentifier" => "782F5EA9-8934-4FFC-88A2-9F37DB0867C5"
      "name" => "Messages.app"
    }
    <snip>
```

Setup
-----
`unarchive_plist.py` must be run on an OS X system with Xcode installed as it utilizes PyObjC (the bridge between Python and Objective-C) for Apple specific classes and objects.

Usage
-----
```
$ python unarchive_plist.py -h
usage: unarchive_plist.py [-h] -r PLIST_IN [-f {xml1,binary1}] -w PLIST_OUT

Convert a keyed archived plist to a serialization with key-value pairs.

optional arguments:
  -h, --help            show this help message and exit
  -r PLIST_IN, --read PLIST_IN
                        Property List (plist or sfl) file to convert.
  -f {xml1,binary1}, --format {xml1,binary1}
                        Output format of plist_out.
  -w PLIST_OUT, --write PLIST_OUT
                        Filename to write the new serialized plist.
```

Example
-------
Convert archived RecentApplications plist to serialized XML plist:

```
$ python unarchive_plist.py \
    -r com.apple.LSSharedFileList.RecentApplications.sfl \
    -f xml1 \
    -w com.apple.LSSharedFileList.RecentApplications_readable.plist
```

Troubleshooting
---------------
`unarchive_plist.py` utilizes [pyobjc](https://bitbucket.org/ronaldoussoren/pyobjc/src) to call Objective-C methods and frameworks. The limitation of pyobjc is that it does not have wrappers for every Framework on OS X or iOS, especially newer ones. This causes `unarchive_plist.py` to throw an error when a class type is unknown by pyobjc:

```
$ python unarchive_plist.py -r StateModel1.archive.plist -w new.plist
[ERROR] NSInvalidUnarchiveOperationException - *** -[NSKeyedUnarchiver decodeObjectForKey:]: cannot decode object of class (RTStateModel) for key (root); the class may be defined in source code or a library that is not linked
```

Future Work
-----------
Future work will be focused on adding newer and missing Frameworks and objects type to pyobjc in order to have more comprehensive support of plist conversion, or porting this project to Objective-C.