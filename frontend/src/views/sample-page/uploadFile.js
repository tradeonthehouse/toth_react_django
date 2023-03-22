import React, { useState } from 'react';
import axios from 'axios';

import configData from '../../config';

// material-ui
import {
    Button,
    Grid,
    TextField,
} from '@material-ui/core';

// project imports
import MainCard from '../../ui-component/cards/MainCard';

//==============================|| SAMPLE PAGE ||==============================//

const UploadFile = () => {
    const [file, setFile] = useState(0);

    const handleFileUpload = (event) => {
        if (event.target.files) {
            setFile(event.target.files[0]);
        }
        console.log(file);
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('excel', file);

        try {
            const response = await axios.post(configData.API_SERVER + 'users/uploadmonthlymodel', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert(response.data.msg);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <MainCard title="Upload File">
            <Grid container spacing={2}>
                <Grid item xs={4}>
                    <TextField type="file" onChange={handleFileUpload} />
                </Grid>
                <Grid item xs={2}>
                    <Button onClick={handleSubmit} variant="contained" component="label" style={{marginTop:5}}>
                        Upload
                    </Button>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default UploadFile;
