"""Convert a keyed archived plist to a serialization with key-value pairs."""

import argparse
import sys

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from Foundation import *
import objc


def nsdict_to_plist(nsdict, plist_name, output_format):
    """Write NSDictionary out to a plist file."""
    # select plist output format
    if output_format == "xml1":
        fmt = NSPropertyListXMLFormat_v1_0
    elif output_format == "binary1":
        fmt = NSPropertyListBinaryFormat_v1_0

    # serialize the NSDictionary
    srl, err = (
        NSPropertyListSerialization.dataWithPropertyList_format_options_error_(
            nsdict, fmt, 0, None))

    if srl:
        # convert NSData object into correct encoding
        if output_format == "xml1":
            plist = NSString.alloc().initWithData_encoding_(
                srl, NSUTF8StringEncoding)
        elif output_format == "binary1":
            plist = bytearray(NSData.alloc().initWithData_(srl))
        try:
            # write string data to file
            with open(plist_name, "wb") as pfile:
                pfile.write(plist)
        except IOError as error:
            print("[ERROR] Failed to write to %s: %s" %
                  (error.filename, error.strerror))
    else:
        print("[ERROR] Failed to serialize NSData as %s: %s" %
              (output_format.upper(), err))


def handle_none(ns_obj):
    """Handle NSObjects being None."""
    if ns_obj is None:
        # NSObjects should be an empty string in type is None
        return ""
    else:
        return ns_obj


def sfllistitem_to_nsdict(sfllistitem):
    """Convert Objective-C Class SFLListItem to an NSDictionary."""
    # SFLListItem format documented here:
    # http://michaellynn.github.io/2015/10/24/apples-bookmarkdata-exposed/
    return handle_none(NSDictionary.dictionaryWithDictionary_({
        "name": handle_none(sfllistitem.name()),
        "uniqueIdentifier": handle_none(
            sfllistitem.uniqueIdentifier().UUIDString()),
        "properties": handle_none(sfllistitem.properties()),
        "bookmark": handle_none(sfllistitem.bookmark())
    }))


def nskeyedarchive_to_nsdict(plist_name):
    """Convert a NSKeyedArchive to a serializable NSDictionary."""
    try:
        # unarchive plist into a nsdict
        nsdict = NSKeyedUnarchiver.unarchiveObjectWithFile_(plist_name)
    except objc.error as err:
        print("[ERROR] %s" % err)
        sys.exit(1)

    if nsdict:
        # read SFLListItem "items" in order and return as list of nsdicts
        items = sorted(nsdict.items())
    else:
        print("[ERROR] Failed to unarchive %s. Check input name." % plist_name)
        sys.exit(1)

    # copy nsdict into a mutable nsdict and update "items"
    new_nsdict = NSMutableDictionary.alloc().init()
    new_nsdict.addEntriesFromDictionary_(nsdict)
    new_nsdict["items"] = items

    return new_nsdict


def parse_arguments():
    """Argument Parser."""
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument(
        "-r",
        "--read",
        dest="plist_in",
        required=True,
        help="Property List (plist or sfl) file to convert.")
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        required=False,
        default="xml1",
        choices=["xml1", "binary1"],
        help="Output format of plist_out.")
    parser.add_argument(
        "-w",
        "--write",
        dest="plist_out",
        required=True,
        help="Filename to write the new serialized plist.")
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    new_nsdict = nskeyedarchive_to_nsdict(args.plist_in)
    nsdict_to_plist(new_nsdict, args.plist_out, args.output_format)


if __name__ == "__main__":
    sys.exit(main())
