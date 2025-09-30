# this script will create a SNOPT firectory and populate it
# with the specified version of the SNOPT source code
# via secure copy over SSH

# The version of SNOPT must be specified via the SNOPT_VERSION environment variable:
#     SNOPT_VERSION=7.7   (for SNOPT 7.7)
#     SNOPT_VERSION=7.2   (for SNOPT 7.2)

# The location of the SNOPT source code must be specified via
# one of the following environment variables:
#     SNOPT_LOCATION_72 (for SNOPT 7.2)
#     SNOPT_LOCATION_77 (for SNOPT 7.7)
#     SNOPT_LOCATION    (for SNOPT 7.7)

if [[ -z "$SNOPT_VERSION" ]]; then
    echo "SNOPT version (7.2 or 7.7) has not been specified, skipping download."
    exit 0
fi

mkdir SNOPT
if [[ "$SNOPT_VERSION" == "7.2" ]]; then
    if [[ -n "$SNOPT_LOCATION_72" ]]; then
        echo "Downloading SNOPT version $SNOPT_VERSION from SNOPT_LOCATION_72 ..."
        scp -v -qr $SNOPT_LOCATION_72 SNOPT
        ls SNOPT
    else
        echo "SNOPT location not found for SNOPT version $SNOPT_VERSION, skipping download."
    fi
else
    if [[ -n "$SNOPT_LOCATION_77" ]]; then
        echo "Downloading SNOPT version $SNOPT_VERSION from SNOPT_LOCATION_77 ..."
        scp -v -qr $SNOPT_LOCATION_77 SNOPT
        ls SNOPT
    elif [[ -n "$SNOPT_LOCATION" ]]; then
        echo "Downloading SNOPT version $SNOPT_VERSION from SNOPT_LOCATION ..."
        scp -v -qr $SNOPT_LOCATION SNOPT
        ls SNOPT
    else
        echo "SNOPT location not found for SNOPT version $SNOPT_VERSION, skipping download."
    fi
fi