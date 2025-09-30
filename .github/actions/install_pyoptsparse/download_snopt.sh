if [ "$SNOPT_VERSION" == "7.7" ]; then
    if [ -n "$SNOPT_LOCATION_77" ]; then
        echo "Downloading SNOPT version $SNOPT_VERSION..."
        scp -qr $SNOPT_LOCATION_77 SNOPT
    elif [ -n "$SNOPT_LOCATION" ]; then
        echo "Downloading SNOPT version $SNOPT_VERSION..."
        scp -qr $SNOPT_LOCATION SNOPT
    else
        echo "SNOPT location not found for SNOPT version $SNOPT_VERSION, skipping download."
    fi
elif [ "$SNOPT_VERSION" == "7.2" ]; then
    if [ -n "$SNOPT_LOCATION_72" ]; then
        echo "Downloading SNOPT version $SNOPT_VERSION..."
        scp -qr $SNOPT_LOCATION_72 SNOPT
    else
        echo "SNOPT location not found for SNOPT version $SNOPT_VERSION, skipping download."
    fi
else
    echo "SNOPT version (7.2 or 7.7) has not been specified, skipping download."
fi