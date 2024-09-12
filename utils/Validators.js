const ValidateNucleotides = (nucleotide) => {
    for (const nt of nucleotide){
        if (!['A', 'T', 'C', 'G'].includes(nt.toUpperCase())) {
            return false;
        }
    } 
    return true;
}

const ValidateCompleteFields = (searchData) => {
    return (searchData.chromosome !== '' && searchData.position !== '' 
            && searchData.reference !== '' && searchData.alternate !== '' 
            && searchData.reference !== searchData.alternate);
}

const ConvertCoordinates = (data) => {
    const validData = {...data};
    if (validData.reference.length > 1){
        const delStart = parseInt(validData.position) + 1;
        // determine if single nucleotide deletion
        if (validData.alternate.length - validData.reference.length === 1){
            validData.notation = `${validData.chromosome}:g.${delStart}del`;
        } else {
            const delEnd = delStart + validData.reference.length - 2;
            validData.notation = `${validData.chromosome}:g.${delStart}_${delEnd}del`;
        }
    } else {
        validData.notation = `${validData.chromosome}:g.${validData.position}${validData.reference.toUpperCase()}%3E${validData.alternate.toUpperCase()}`;
    }
    return validData;
};

export { ValidateNucleotides, ValidateCompleteFields, ConvertCoordinates };