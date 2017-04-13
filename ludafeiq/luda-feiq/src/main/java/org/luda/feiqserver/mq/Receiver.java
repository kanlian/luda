package org.luda.feiqserver.mq;/*
 * Copyright 2017 Luda Team.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * Created by Him on 2017/4/13.
 */

import org.jplus.jfeiq.feiq.FeiqServer;
import org.jplus.jfeiq.feiq.IPMSGData;
import org.luda.feiqserver.Application;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageListener;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;

@Component
public class Receiver implements MessageListener {
    private static final Logger logger = LoggerFactory.getLogger(Receiver.class);
    private CountDownLatch latch = new CountDownLatch(1);
    //飞秋服务
    private FeiqServer feiqServer = Application.feiq.getFeiqServer();

    public void receiveMessage(String message) {
        logger.info("Received <" + message + ">");
    }

    public CountDownLatch getLatch() {
        return latch;
    }

    @Override
    public void onMessage(Message message) {
        logger.info("Received <" + message.toString() + ">");
        String msg = new String(message.getBody());
        IPMSGData MSG = new IPMSGData(32, msg, "192.168.100.165");
        feiqServer.sendMsg(MSG);
        latch.countDown();
    }
}
