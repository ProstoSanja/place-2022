import { useEffect, useState } from "react";
import * as dayjs from 'dayjs'

function Timer() {

    const [time, setTime] = useState(calculateTime());
    useEffect(() => {
        const interval = setInterval(() => setTime(calculateTime()), 1000);
        console.log("Setting interval")
        return function cleanup() {
            console.log("clearing interval")
            clearInterval(interval);
        };
    }, []);

    return (
        <span>{time}</span>
    );
}

const start = dayjs('2022-04-02T14:00:00.000Z');

function calculateTime() {
    let now = dayjs()
    return now.subtract(start).format('D [day] H [hours] m [minutes and] s [seconds]')
}

export default Timer;
