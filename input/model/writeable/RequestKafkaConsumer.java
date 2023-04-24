package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.core.consumer.shared.resource.event.EventRequestKafkaConsumer;
import no.fintlabs.kafka.event.EventConsumerFactoryService;
import org.springframework.stereotype.Service;

@Service
public class MODELRequestKafkaConsumer extends EventRequestKafkaConsumer<MODEL_RESOURCE> {
    public MODELRequestKafkaConsumer(EventConsumerFactoryService eventConsumerFactoryService, MODELConfig MODEL_LOWERConfig) {
        super(eventConsumerFactoryService, MODEL_LOWERConfig);
    }
}
