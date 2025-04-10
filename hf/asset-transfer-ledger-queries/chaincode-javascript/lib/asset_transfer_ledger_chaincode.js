'use strict';

const { Contract } = require('fabric-contract-api');

class Chaincode extends Contract {

    // CreateProfile - create a new profile and store it into the ledger
    async CreateProfile(ctx, campusID, name, email, department, fe) {
        const exists = await this.ProfileExists(ctx, campusID);
        if (exists) {
            throw new Error(`The profile ${campusID} already exists`);
        }

        // Create profile object and marshal to JSON
        let profile = {
            docType: 'profile',
            campusID: campusID,
            name: name,
            email: email,
            department: department,
            fe: fe, // Add facial embeddings
            time: new Date().toISOString(), // Set the current time
        };

        // Save profile to state
        await ctx.stub.putState(campusID, Buffer.from(JSON.stringify(profile)));

        // Create an index to enable efficient name-based queries
        let indexName = 'name~campusID';
        let nameCampusIDIndexKey = await ctx.stub.createCompositeKey(indexName, [profile.name, profile.campusID]);

        // Save index entry to state (value is a null character)
        await ctx.stub.putState(nameCampusIDIndexKey, Buffer.from('\u0000'));
    }

    // ReadProfile returns the profile stored in the ledger with the given campusID
    async ReadProfile(ctx, campusID) {
        const profileJSON = await ctx.stub.getState(campusID);
        if (!profileJSON || profileJSON.length === 0) {
            throw new Error(`Profile ${campusID} does not exist`);
        }

        return profileJSON.toString();
    }

    // DeleteProfile removes a profile from the ledger
    async DeleteProfile(ctx, campusID) {
        if (!campusID) {
            throw new Error('Campus ID must not be empty');
        }

        const exists = await this.ProfileExists(ctx, campusID);
        if (!exists) {
            throw new Error(`Profile ${campusID} does not exist`);
        }

        // Retrieve the profile to get its name (needed to delete the composite key)
        const profileJSON = await ctx.stub.getState(campusID);
        let profile;
        try {
            profile = JSON.parse(profileJSON.toString());
        } catch (err) {
            throw new Error(`Failed to decode JSON of: ${campusID}`);
        }

        await ctx.stub.deleteState(campusID); // Remove the profile from state

        // Delete the composite key index
        let indexName = 'name~campusID';
        let nameCampusIDIndexKey = ctx.stub.createCompositeKey(indexName, [profile.name, profile.campusID]);
        if (!nameCampusIDIndexKey) {
            throw new Error('Failed to create the composite key');
        }
        await ctx.stub.deleteState(nameCampusIDIndexKey);
    }

    // UpdateProfile updates an existing profile in the ledger
    async UpdateProfile(ctx, campusID, name, email, department, fe) {
        const exists = await this.ProfileExists(ctx, campusID);
        if (!exists) {
            throw new Error(`Profile ${campusID} does not exist`);
        }

        // Retrieve the current profile
        const profileJSON = await ctx.stub.getState(campusID);
        let profile;
        try {
            profile = JSON.parse(profileJSON.toString());
        } catch (err) {
            throw new Error(`Failed to decode JSON of: ${campusID}`);
        }

        // Delete the old composite key entry if the name has changed
        if (profile.name !== name) {
            let oldIndexName = 'name~campusID';
            let oldNameCampusIDIndexKey = ctx.stub.createCompositeKey(oldIndexName, [profile.name, profile.campusID]);
            await ctx.stub.deleteState(oldNameCampusIDIndexKey);
        }

        // Update the profile fields
        profile.name = name;
        profile.email = email;
        profile.department = department;
        profile.fe = fe; // Update facial embeddings
        profile.time = new Date().toISOString(); // Update the time to current time

        // Save the updated profile to state
        await ctx.stub.putState(campusID, Buffer.from(JSON.stringify(profile)));

        // Create new composite key with updated name
        let indexName = 'name~campusID';
        let nameCampusIDIndexKey = ctx.stub.createCompositeKey(indexName, [profile.name, profile.campusID]);
        await ctx.stub.putState(nameCampusIDIndexKey, Buffer.from('\u0000'));
    }

    // GetProfilesByRange performs a range query based on the start and end keys provided
    async GetProfilesByRange(ctx, startKey, endKey) {
        const resultsIterator = await ctx.stub.getStateByRange(startKey, endKey);
        const results = await this._GetAllResults(resultsIterator, false);

        return JSON.stringify(results);
    }

    // QueryProfilesByDepartment queries for profiles based on a department
    async QueryProfilesByDepartment(ctx, department) {
        const queryString = {
            selector: {
                docType: 'profile',
                department: department,
            },
        };
        return await this.GetQueryResultForQueryString(ctx, JSON.stringify(queryString));
    }

    // QueryProfiles executes a query string to perform a query for profiles
    async QueryProfiles(ctx, queryString) {
        return await this.GetQueryResultForQueryString(ctx, queryString);
    }

    // GetQueryResultForQueryString executes the passed-in query string
    async GetQueryResultForQueryString(ctx, queryString) {
        const resultsIterator = await ctx.stub.getQueryResult(queryString);
        const results = await this._GetAllResults(resultsIterator, false);

        return JSON.stringify(results);
    }

    // GetProfileHistory returns the history of a profile (chain of custody)
    async GetProfileHistory(ctx, campusID) {
        const resultsIterator = await ctx.stub.getHistoryForKey(campusID);
        const results = await this._GetAllResults(resultsIterator, true);

        return JSON.stringify(results);
    }

    // ProfileExists returns true if a profile with the given campusID exists in the ledger
    async ProfileExists(ctx, campusID) {
        const profileJSON = await ctx.stub.getState(campusID);
        return profileJSON && profileJSON.length > 0;
    }

    // Internal method to fetch all results from an iterator
    async _GetAllResults(iterator, isHistory) {
        const allResults = [];
        let res = await iterator.next();
        while (!res.done) {
            const jsonRes = {};
            if (res.value && res.value.value.toString()) {
                if (isHistory) {
                    jsonRes.TxId = res.value.txId;
                    jsonRes.Timestamp = res.value.timestamp;
                    try {
                        jsonRes.Value = JSON.parse(res.value.value.toString('utf8'));
                    } catch (err) {
                        jsonRes.Value = res.value.value.toString('utf8');
                    }
                } else {
                    jsonRes.Key = res.value.key;
                    try {
                        jsonRes.Record = JSON.parse(res.value.value.toString('utf8'));
                    } catch (err) {
                        jsonRes.Record = res.value.value.toString('utf8');
                    }
                }
                allResults.push(jsonRes);
            }
            res = await iterator.next();
        }
        await iterator.close();
        return allResults;
    }

    // InitLedger creates sample profiles in the ledger
    async InitLedger(ctx) {
        const profiles = [
            {
                campusID: 'profile1',
                name: 'Alice',
                email: 'alice@example.com',
                department: 'Engineering',
                fe: 'facial_embedding_data_1', // Sample facial embedding data
            },
            {
                campusID: 'profile2',
                name: 'Bob',
                email: 'bob@example.com',
                department: 'Marketing',
                fe: 'facial_embedding_data_2',
            },
            {
                campusID: 'profile3',
                name: 'Charlie',
                email: 'charlie@example.com',
                department: 'Sales',
                fe: 'facial_embedding_data_3',
            },
            {
                campusID: 'profile4',
                name: 'Diana',
                email: 'diana@example.com',
                department: 'HR',
                fe: 'facial_embedding_data_4',
            },
            {
                campusID: 'profile5',
                name: 'Eve',
                email: 'eve@example.com',
                department: 'Finance',
                fe: 'facial_embedding_data_5',
            },
            {
                campusID: 'profile6',
                name: 'Frank',
                email: 'frank@example.com',
                department: 'IT',
                fe: 'facial_embedding_data_6',
            },
        ];

        for (const profile of profiles) {
            await this.CreateProfile(
                ctx,
                profile.campusID,
                profile.name,
                profile.email,
                profile.department,
                profile.fe
            );
        }
    }
}

module.exports = Chaincode;
