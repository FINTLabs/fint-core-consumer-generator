package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.core.consumer.shared.resource.kafka.EntityKafkaConsumer;
import no.fintlabs.kafka.common.ListenerBeanRegistrationService;
import no.fintlabs.kafka.entity.EntityConsumerFactoryService;
import no.fintlabs.kafka.entity.topic.EntityTopicService;
import org.springframework.stereotype.Service;

@Service
public class MODELKafkaConsumer extends EntityKafkaConsumer<MODEL_RESOURCE> {
    public MODELKafkaConsumer(
            EntityConsumerFactoryService entityConsumerFactoryService,
            ListenerBeanRegistrationService listenerBeanRegistrationService,
            EntityTopicService entityTopicService,
            MODELConfig MODEL_LOWERConfig) {
        super(entityConsumerFactoryService,
                listenerBeanRegistrationService,
                entityTopicService,
                MODEL_LOWERConfig);
    }
}
